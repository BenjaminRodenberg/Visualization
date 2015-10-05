pub_zmqaddr ="ipc:///tmp/0"
sub_zmqaddr ="ipc:///tmp/1"
run_forwarder = False
model_backend = {'type' : 'redis', 'redis_port' : 7001, 'start-redis' : True}
secret_key = "foobarbaz"
multi_user = True
scripts = ["run_app.py"]
