# Flask server example with Redis DB
[Project link](https://github.com/stepvg/crud_api_compose_example)

## How to run
* Install Git and Docker Compose
> `sudo apt install git docker-compose`
* Add current user to Docker group
> `sudo usermod $(whoami) -a -G docker`
* Download current repository
> `git clone https://github.com/stepvg/crud_api_compose_example.git`
> `cd crud_api_compose_example/`
* Run [install.sh](install.sh) (systemd service requires sudo)
> `./install.sh`
* You can use Curl to monitor the operation of the memory_notifier.py script.
> `curl -v -X GET http://localhost:8080/memory/use`

**All parameters are hardcoded to make the example as easy as possible** 

## Source code
* [Docker Compose file](docker-compose.yml) describes the Redis server and the Flask server
* [Python file](flask_redis_editor/flask_redis_editor.py) contains the Flask server API logic
* [Dockerfile](flask_redis_editor/Dockerfile) describes the Docker image that is used to run Flask server
* [Python file](memory_notifier/memory_notifier.py) contains a script for monitoring memory usage.

