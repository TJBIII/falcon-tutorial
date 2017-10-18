# falcon-tutorial
Tutorial for the [Falcon](https://github.com/falconry/falcon) framework. Follows the tutorial closely but also adds some more tests and a dockerized app.

# Start server
```
$ TUTORIAL_STORAGE_PATH=/tmp gunicorn --reload 'tutorial.app:get_app()'
```

# Run tests
```
$ TUTORIAL_STORAGE_PATH=/tmp pytest tests
```
