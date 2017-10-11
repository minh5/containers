import os

from invoke import task

DEFAULTS = {
    'PROJECT': os.environ.get('GCE_PROJ'),
    'ZONE': os.environ.get('GCE_ZONE'),
    'N_NODES': 4
}

@task
def start(ctx, machine='n1-standard-2'):
    cmd = """
    gcloud alpha container clusters create instances \
        --machine-type "{machine}" \
        --num-nodes "{nnodes}" \
        --zone {zone} \
        --project "{project}" \
        --enable-autoscaling \
        --min-nodes 1 \
        --max-nodes 8 \
        --preemptible
    """.format(
        machine=machine,
        zone=DEFAULTS['ZONE'],
        project=DEFAULTS['PROJECT'],
        nnodes=DEFAULTS['N_NODES']
    )
    ctx.run(cmd, echo=True)

def get_instance_group(ctx):
    stdout = ctx.run('gcloud compute instance-groups list').stdout
    return stdout.split('\n')[1].split()[0] 

@task
def add_to_firewall(ctx):
    pass

@task
def stop(ctx):
    grp = get_instance_group(ctx)
    ctx.run('gcloud compute instance-groups managed delete %s' % grp, echo=True)