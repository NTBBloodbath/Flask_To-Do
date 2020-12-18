# NTBBloodbath – Flask To-Do
# Flask To-Do is distributed under WTFPL License.
# =======================================================
# I did this project to learn how to use Flask and Redis
# and I decided to release the code as it may be useful
# to others who are also learning.
#
# Documentation
# =============
# • Flask
#   https://flask.palletsprojects.com/en/master/
# • Bootstrap (v5)
#   https://getbootstrap.com/docs/5.0/getting-started/introduction/
# • Redis
#   https://redis.io/documentation
#
# Redis methods used
# ==================
# • StrictRedis (Constructor)
#   alias of redis.client.Redis
#   Docs: https://redis-py.readthedocs.io/en/stable/#redis.StrictRedis
# • FLUSHDB
#   Delete all the keys of the currently selected DB. This command never fails.
#   Docs: https://redis.io/commands/flushdb
# • LLEN
#   Returns the length of the list stored at key.
#   Docs: https://redis.io/commands/llen
# • LRANGE
#   Returns the specified elements of the list stored at key.
#   Docs: https://redis.io/commands/lrange
# • RPUSH
#   Insert all the specified values at the tail of the list stored at key.
#   Docs: https://redis.io/commands/rpush
# • LINDEX
#   Returns the element at index index in the list stored at key.
#   Docs: https://redis.io/commands/lindex
# • LSET
#   Sets the list element at index to element.
#   Docs: https://redis.io/commands/lset
# • LREM
#   Removes the first count occurrences of elements equal to element from the list stored at key.
#   Docs: https://redis.io/commands/lrem

import redis
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# configure the Redis client to automatically convert responses
# from bytes to strings using the decode_responses argument
# to the StrictRedis constructor.
db = redis.StrictRedis("localhost", charset="utf-8", decode_responses=True)

# Uncomment this line if you want to restart the entire database
# when starting / restarting the Flask server.
# db.flushdb()

# local tasks list.
# =================
# If the list of tasks in the database is empty,
# it will be the same when starting the server.
if db.llen("tasks"):
    tasks = db.lrange("tasks", 0, -1)
else:
    tasks = []


@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["GET", "POST"])
def add_or_render():
    if request.method == "POST":
        try:
            # Raise error if task is an empty string
            if not request.form.get("task"):
                return "<h1>500 Internal Server Error</h1><p>The task must be longer than 1 character</p>"
            # Pushes the task obtained from the form to the tail of the list (in the database)
            db.rpush("tasks", request.form.get("task"))
            # Pushes the task obtained from the form to the tail of the list (in the local tasks)
            tasks.append(db.lindex("tasks", -1))
            return redirect("/")
        except Exception as err:
            return f"<h1>500 Internal Server Error</h1><p>{err}</p>"
    else:
        return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit_or_render():
    if request.method == "POST":
        try:
            # Raise error if new_task is an empty string
            if not request.form.get("new_task"):
                return "<h1>500 Internal Server Error</h1><p>The new task must be longer than 1 character</p>"
            # Search the database tasks list for the old value and replace it with the new one
            for i in range(0, db.llen("tasks")):
                # If the current index value is equal to the selected task
                # then update the index value to the new value.
                if db.lindex("tasks", i) == request.form.get("task"):
                    db.lset("tasks", i, request.form.get("new_task"))
            # Search local tasks list for the old value and replace it with the new one.
            for i, _ in enumerate(tasks):
                if tasks[i] == request.form.get("task"):
                    tasks[i] = request.form.get("new_task")
            return redirect("/")
        except Exception as err:
            return f"<h1>500 Internal Server Error</h1><p>{err}</p>"
    else:
        return render_template("edit.html", tasks=tasks)


@app.route("/delete", methods=["GET", "POST"])
def delete_or_render():
    if request.method == "POST":
        try:
            # Obtain through the form checkboxes the tasks to be deleted.
            tasks_to_delete = request.form.to_dict()

            for task in tasks_to_delete.keys():
                for i in range(0, db.llen("tasks")):
                    # If the index value isn't None and is equal to one of the tasks to delete then delete it.
                    if db.lindex("tasks", i) is not None and db.lindex("tasks", i) == task:
                        db.lrem("tasks", 0, task)
                        tasks.remove(task)
            return redirect("/")
        except Exception as err:
            return f"<h1>500 Internal Server Error</h1><p>{err}</p>"
    else:
        return render_template("delete.html", tasks=tasks)


# Restart the Flask server with every change to this script.
# NOTE: use this conditional only in development environment.
if __name__ == "__main__":
    app.run(debug=True)
