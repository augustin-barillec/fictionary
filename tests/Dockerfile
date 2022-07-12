FROM cypress/included:10.0.2
COPY package.json .
COPY package-lock.json .
RUN npm install

RUN apt-get install python3-venv -y
ENV VENV=/opt/venv
RUN rm -rf $VENV
RUN python3 -m venv $VENV --copies
ENV PATH="$VENV/bin:$PATH"
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install -r requirements.txt
