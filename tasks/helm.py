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
def configure(ctx):
    # helm lint <chart>
    # helm dep update <chart>
    # helm package <chart>
    # helm repo index . --url {gs url}
    # gsutil-m rsync . $GS_REPO
    # helm repo update
    pass

def _install(ctx, name):
    chart_path = DEFAULTS['CHARTS_DIR'] + name
    ctx.run('helm install --name %s %s' % (name, chart_path), echo=True)

def _delete(ctx, name):
    ctx.run('helm del --purge %s' % (name), echo=True)

