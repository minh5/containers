import os

from invoke import task

from .helm import _delete, _install

DEFAULTS = {
    'MEM': 8192,
    'DISK_SIZE': '20g',
    'CPUS': 4
}


@task
def start(ctx, driver='xhyve'):
    cmd = """
    minikube start --vm-driver={driver} \
    --memory={memory} \
    --cpus={cpus} \
    --disk-size={size} \
    """.format(
        driver=driver,
        memory=DEFAULTS['MEM'],
        cpus=DEFAULTS['CPUS'],
        size=DEFAULTS['DISK_SIZE']
    )
    ctx.run(cmd, echo=True)

@task
def stop(ctx):
    ctx.run('minikube stop', echo=True)

@task
def install(ctx, name):
    if name == 'all':
        for chart in os.listdir('~/sandbox/charts/'):
            _install(ctx, chart)
    else:
        _install(ctx, name)

@task
def delete(ctx, name):
    if name == 'all':
        for chart in os.listdir('~/sandbox/charts/'):
            _delete(ctx, chart)
    else:
        _delete(ctx, name)

@task
def reinstall(ctx, name):
    if name == 'all':
        for chart in os.listdir('~/sandbox/charts/'):
            _delete(ctx, chart)
            _install(ctx, chart)
    else:
        _delete(ctx, name)
        _install(ctx, name)