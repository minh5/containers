import os

from invoke import task

DEFAULTS = {
    'PROJECT': os.environ.get('GCE_PROJ'),
    'ZONE': os.environ.get('GCE_ZONE'),
    'N_NODES': 4,
    'MACHINE': 'n1-standard-2'
}

@task
def start(ctx,  name=None):
    cmd = """
    gcloud alpha container clusters create {name} \
        --machine-type "{machine}" \
        --num-nodes "{nnodes}" \
        --zone {zone} \
        --project "{project}" \
        --enable-autoscaling \
        --min-nodes 1 \
        --max-nodes 8 \
        --preemptible
    """.format(
        name=name,
        machine=DEFAULTS['MACHINE'],
        nnodes=DEFAULTS['N_NODES'],
        zone=DEFAULTS['ZONE'],
        project=DEFAULTS['PROJECT'],
    )
    ctx.run(cmd, echo=True)

def get_cluster_name(ctx):
    stdout = ctx.run('gcloud alpha container clusters list').stdout
    return stdout.split('\n')[1].split()[0] 

@task
def add_to_firewall(ctx):
    pass

@task
def stop(ctx):
    grp = get_cluster_name(ctx)
    ctx.run('gcloud alpha container clusters delete %s' % grp, echo=True)