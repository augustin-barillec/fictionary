import yaml
from utils import split

DOCKER_IMAGE = \
    'europe-west1-docker.pkg.dev/$PROJECT_ID/from-dockerfile/tests_image'


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


class Writer:

    def __init__(
            self,
            destination_file_path,
            docker_image):
        self.destination_file_path = destination_file_path
        self.docker_image = docker_image

    @property
    def content(self):
        return None

    def build_step(
            self,
            args,
            entrypoint=None,
            dir_=None,
            wait_for=None,
            id_=None,
            name=None):
        res = {'args': args}
        if entrypoint is not None:
            res['entrypoint'] = entrypoint
        if dir_ is not None:
            res['dir'] = dir_
        if wait_for is not None:
            res['waitFor'] = wait_for
        if id_ is not None:
            res['id'] = id_
        if name is not None:
            res['name'] = name
        else:
            res['name'] = self.docker_image
        return res

    def write(self):
        with open(self.destination_file_path, 'w') as f:
            yaml.dump(self.content, f, Dumper=NoAliasDumper)


class SubRunTestsWriter(Writer):

    def __init__(
            self,
            destination_file_path,
            sources):
        super().__init__(destination_file_path, DOCKER_IMAGE)
        self.destination_file_path = destination_file_path
        self.sources = sources

    def build_dummy_step(self):
        return self.build_step(
            args=['$_BUCKET_DIR_NAME'], entrypoint='echo', dir_='tests')

    def build_run_cypress_step(self, source):
        args = ['run.py', '$PROJECT_ID', 'tests-$PROJECT_ID',
                '$_BUCKET_DIR_NAME', 'run_cypress', source, '23']
        return self.build_step(
            args=args, entrypoint='python', dir_='tests')

    def build_steps(self):
        res = [self.build_dummy_step()]
        res += [self.build_run_cypress_step(s) for s in self.sources]
        return res

    @property
    def content(self):
        steps = self.build_steps()
        content = {'steps': steps, 'timeout': '3600s'}
        return content


class RunTestsWriter(Writer):

    def __init__(
            self,
            no_parallelizable_sources,
            parallelizable_sources,
            nb_batches):
        super().__init__(
            'run_tests.yaml',
            DOCKER_IMAGE)
        self.no_parallelizable_sources = no_parallelizable_sources
        self.parallelizable_sources = parallelizable_sources
        self.nb_batches = nb_batches
        self.parallelizable_batches = split.split(
            self.parallelizable_sources, self.nb_batches)
        self.nb_expected_cases = (
                len(self.no_parallelizable_sources) +
                len(self.parallelizable_sources))
        self.sub_run_tests_file_path_template = 'sub_run_tests_{i}.yaml'

    def build_run_cypress_step(self, source):
        args = ['run.py', '$PROJECT_ID',
                'tests-$PROJECT_ID', '$BUILD_ID',
                'run_cypress', source, '23']
        return self.build_step(
            args=args, entrypoint='python', dir_='tests')

    def build_submit_step(self, i):
        cloudbuild_file_path = \
            f'cloudbuild/{self.sub_run_tests_file_path_template.format(i=i)}'
        args = ['builds', 'submit', '.',
                '--config', cloudbuild_file_path,
                '--region', 'europe-west1',
                '--gcs-source-staging-dir',
                'gs://cloudbuild-$PROJECT_ID/source',
                '--async',
                '--substitutions', f'_BUCKET_DIR_NAME=$BUILD_ID']
        entrypoint = 'gcloud'
        return self.build_step(
            args=args,
            entrypoint=entrypoint,
            name='gcr.io/cloud-builders/gcloud')

    def build_wait_end_step(self):
        args = ['run.py', '$PROJECT_ID',
                'tests-$PROJECT_ID', '$BUILD_ID',
                'wait_end', f'{self.nb_expected_cases}']
        return self.build_step(
            args=args, entrypoint='python', dir_='tests')

    def build_write_stats_step(self):
        args = ['run.py', '$PROJECT_ID',
                'tests-$PROJECT_ID', '$BUILD_ID',
                'write_stats']
        return self.build_step(
            args=args, entrypoint='python',  dir_='tests')

    def build_report_successes_step(self):
        args = ['run.py', '$PROJECT_ID',
                'tests-$PROJECT_ID', '$BUILD_ID',
                'report_successes']
        return self.build_step(args=args, entrypoint='python', dir_='tests')

    def build_report_fails_step(self):
        args = ['run.py', '$PROJECT_ID',
                'tests-$PROJECT_ID', '$BUILD_ID',
                'report_fails']
        return self.build_step(args=args, entrypoint='python', dir_='tests')

    def build_steps(self):
        res = []
        for s in self.no_parallelizable_sources:
            step = self.build_run_cypress_step(s)
            res.append(step)
        for i in range(1, len(self.parallelizable_batches) + 1):
            step = self.build_submit_step(i)
            res.append(step)
        res.append(self.build_wait_end_step())
        res.append(self.build_write_stats_step())
        res.append(self.build_report_successes_step())
        res.append(self.build_report_fails_step())
        return res

    @property
    def content(self):
        steps = self.build_steps()
        content = {'steps': steps, 'timeout': '7200s'}
        return content

    def instantiate_sub_run_tests_writer(self, i, sources):
        res = SubRunTestsWriter(
                self.sub_run_tests_file_path_template.format(i=i),
                sources)
        return res

    def write(self):
        super().write()
        for i, batch in enumerate(self.parallelizable_batches, 1):
            self.instantiate_sub_run_tests_writer(i, batch).write()
