import os

from invoke import task

DEFAULTS = {
    'PROJECT': os.environ.get('GCE_PROJ_ID'),
    'ZONE': os.environ.get('GCE_ZONE'),
    'N_NODES': 4
}

@task
def start(ctx, machine='n1-standard-1'):
    cmd = """
    gcloud alpha container clusters create instances \
        --machine-type "{machine}" \
        --num-nodes "{nnodes}" \
        --zone {zone} \
        --project "{project}"
        --preemptible
    """.format(
        machine=machine,
        zone=DEFAULTS['ZONE'],
        project=DEFAULTS['PROJECT'],
        nnodes=DEFAULTS['N_NODES']
    )
    ctx.run(cmd, echo=True)


@task
def add_to_firewall(ctx):
    pass

@task
def stop(ctx):
    pass