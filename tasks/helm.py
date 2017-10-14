import os
from invoke import task

DEFAULTS = {
     'CHARTS_DIR':'$HOME/sandbox/charts/'
}

@task
def init(ctx):
    ctx.run('helm init', echo=True)

def _install(ctx, name):
    chart_path = DEFAULTS['CHARTS_DIR'] + name
    ctx.run('helm install --name %s %s' % (name, chart_path), echo=True)

@task
def install(ctx, name='all'):
    if name == 'all':
        for chart in os.listdir('~/sandbox/charts/'):
            _install(ctx, chart)
    else:
        _install(ctx, name)

def _delete(ctx, name):
    ctx.run('helm delete %s' % (name), echo=True)

@task
def delete(ctx, name='all'):
    if name == 'all':
        for chart in os.listdir('~/sandbox/charts/'):
            _delete(ctx, chart)
    else:
        _delete(ctx, name)