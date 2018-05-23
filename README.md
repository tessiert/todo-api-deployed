
<p align="center">
  <img width="460" src="https://media.giphy.com/media/2wU5k2zFA4nvvSMjfR/giphy.gif">
</p>
<p align="center">
  <b><a href="https://wdc-class-8-rest-api-deployed.herokuapp.com/" target="_blank">Live Demo</a></b>
</p>

### Final Project: API from Scratch + Heroku Deploy

In this project you're in charge of integrating an API to your service, and deploying it to Heroku.

Most of the project's functionality is already done: both models and frontend are built. We've also included an admin user and a few model instances to have data to get started

##### Setup Instruction

```bash
$ mkvirtualenv todos-api -p /usr/bin/python3
$ pip install -r dev-requirements.txt
$ make migrate
```

You can now run the development server:

```bash
$ make runserver
```

And point your browser to the correct URL and should see already the todos working. There's a superuser created with username `admin` and password `admin`.

### Your Tasks

Your job is to implement the API that's under `todos_app/api.py`. URLs and models are already done. The tests are under `tests/`. Suggested path:

* `test_list_get.py`
* `test_detail_get.py`
* `test_list_post.py`
* `test_detail_delete.py`
* `test_detail_put.py`
* `test_detail_patch.py`

To run tests:

```bash
$ py.test tests/test_list_get.py
$ py.test tests/test_list_get.py -k test_todo_list
```

##### How to regenerate the DB?

The Database is already provided, but if you need to regenerate it, just run:

```bash
$ rm -f django_todos/django_todos/db.sqlite3  # WARNING: deleting previous DB.
$ make migrate
$ python load_initial_data.py
```
