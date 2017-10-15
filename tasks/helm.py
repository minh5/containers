import os
from invoke import task

DEFAULTS = {
     'CHARTS_DIR':'$HOME/sandbox/charts/',
     'GS_REPO': os.environ.get('GS_REPO'),
     'GS_URL': os.environ.get('GS_URL')
}

@task
def init(ctx):
    ctx.run('helm init', echo=True)

@task
def add_repo(ctx):
    # helm lint <chart>
    # helm dep update <chart>
    # helm package <chart>
    # helm repo index . --url {gs url}
    # gsutil-m rsync . gs://us.artifacts.upbeat-palace-178323.appspot.com
    # helm repo update
    pass

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
    ctx.run('helm del --purge %s' % (name), echo=True)

@task
def delete(ctx, name='all'):
    if name == 'all':
        for chart in os.listdir('~/sandbox/charts/'):
            _delete(ctx, chart)
    else:
        _delete(ctx, name)

@task
def reinstall(ctx, name='all'):
    if name == 'all':
        for chart in os.listdir('~/sandbox/charts/'):
            _delete(ctx, chart)
            _install(ctx, chart)
    else:
        _delete(ctx, name)
        _install(ctx, name)