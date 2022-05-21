import tools
import logging

logger = logging.getLogger(__name__)


class StageTriggerer:

    def __init__(self, publisher, project_id, game_id):
        self.publisher = publisher
        self.project_id = project_id
        self.game_id = game_id

    def build_topic_path(self, topic_name):
        return self.publisher.topic_path(self.project_id, topic_name)

    def publish(self, topic_name):
        topic_path = self.build_topic_path(topic_name)
        future = self.publisher.publish(
            topic_path,
            data='no_data'.encode('utf-8'),
            game_id=self.game_id)
        future.result()

    def trigger_stage(self, port):
        n = tools.ports.port_to_function_name[port]
        topic_name = tools.pubsub_names.topic.format(function_name=n)
        self.publish(topic_name)

    def trigger_pre_guess_stage(self):
        self.trigger_stage(5002)

    def trigger_guess_stage(self):
        self.trigger_stage(5003)

    def trigger_pre_vote_stage(self):
        self.trigger_stage(5004)

    def trigger_vote_stage(self):
        self.trigger_stage(5005)

    def trigger_pre_result_stage(self):
        self.trigger_stage(5006)

    def trigger_result_stage(self):
        self.trigger_stage(5007)
