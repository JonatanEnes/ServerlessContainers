# /usr/bin/python
import src.StateDatabase.couchdb as couchDB
import src.StateDatabase.utils as couchdb_utils

base_container = dict(
    type='structure',
    subtype='container',
    guard_policy="serverless",
    host='host0',
    host_rescaler_ip='host0',
    host_rescaler_port='8000',
    name="base_container",
    guard=False,
    resources=dict(
        cpu=dict(max=600, min=75, guard=True),
        mem=dict(max=46080, min=1024, guard=True),
        disk=dict(max=100, min=20, guard=False),
        net=dict(max=200, min=100, guard=False),
        energy=dict(max=20, min=0, guard=False)
    )
)

base_host = dict(
    type='structure',
    subtype='host',
    name="host0",
    host="host0",
    resources=dict(
        cpu=dict(max=2400),
        mem=dict(max=184320)
    )
)


if __name__ == "__main__":
    initializer_utils = couchdb_utils.CouchDBUtils()
    handler = couchDB.CouchDBServer()
    database = "structures"
    initializer_utils.remove_db(database)
    initializer_utils.create_db(database)

    containers = [("node0","host0"), ("node1","host0"), ("node2","host0"), ("node3","host0"),
                  ("node4", "host1"), ("node5", "host1"), ("node6", "host1"), ("node7", "host1"),
                  ("node8", "host2"), ("node9", "host2"), ("node10", "host2"), ("node11", "host2"),
                  ("node12", "host3"), ("node13", "host3"), ("node14", "host3"), ("node15", "host3")]
    hosts = ["host0","host1","host2","host3"]

    # CREATE STRUCTURES
    if handler.database_exists("structures"):
        print("Adding 'structures' documents")
        for (c, h) in containers:
            container = dict(base_container)
            container["name"] = c
            container["host"] = h
            container["host_rescaler_ip"] = h
            handler.add_structure(container)

        for h in hosts:
            host = dict(base_host)
            host["name"] = h
            host["host"] = h
            handler.add_structure(host)

        app = dict(
            type='structure',
            subtype='application',
            name="app1",
            guard=True,
            guard_policy="serverless",
            resources=dict(
                cpu=dict(max=9600, min=1600, guard=False),
                mem=dict(max=737280, min=163840, guard=False),
                disk=dict(max=600, min=120, guard=False),
                net=dict(max=1200, min=600, guard=False),
                energy=dict(max=800, min=0, shares=100, guard=True)
            ),
            containers=["node0", "node1", "node2", "node3",
                        "node4", "node5", "node6", "node7",
                        "node8", "node9", "node10", "node11",
                        "node12", "node13", "node14", "node15"]
        )
        handler.add_structure(app)