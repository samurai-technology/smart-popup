# Samurai Technology

This is a [Samurai Technology](http://samurai.technology) project.

Contact us at [hi@samurai.technology](mailto:hi@samurai.technology).

![Samurai Technology logo](static/samurai-logo.png)

## Smart popup

Smart popup provides an advice whether to show or not a pop-up. The advice is based on ML models trained on website's 
users activity data (which are not open-sourced).


### Run

1. Provide models and configure their path in ``app/config.ini`` file.
2. Create docker network: ``./bin/docker-create-network.sh``
3. Create backend image: ``./bin/docker-build-backend.sh``
2. Run database: ``./bin/docker-run-database.sh``
3. Run backend: ``./bin/docker-run-backend.sh``

App will be available at ``localhost:8888``.

### Development

While installing new dependencies, remember to update ``app/requirements.txt`` file.

#### IDE
PyCharm (https://www.jetbrains.com/pycharm/) will do.
