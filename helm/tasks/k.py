import os

from invoke import task

DEFAULTS = {
    'NAMESPACE': 'sandbox',
    'EMAIL': 'minh.v.mai@gmail.com',
    'GCE_KEY': os.environ.get('GCE_KEY')
}

@task
def create_secret(ctx):
    cmd = (
        'kubectl --namespace={namespace} '
        'create secret docker-registry gcr-json-key '
        '--docker-server="https://us.gcr.io" '
        '--docker-username=_json_key '
        '--docker-password="$(cat {keyfile_path})" '
        '--docker-email={email}'
    ).format(
        namespace=DEFAULTS['NAMESPACE'],
        keyfile_path='/Users/minhmai/sandbox/%s' % DEFAULTS['GCE_KEY'],
        email=DEFAULTS['EMAIL']
    )
    ctx.run(cmd, echo=True)

@task
def patch_sa(ctx):
    cmd = (
        'kubectl --namespace=%s '
        'patch serviceaccount default -p '
        """ '{"imagePullSecrets": [{"name": "gcr-json-key"}]}' """
    ) % DEFAULTS['NAMESPACE']
    ctx.run(cmd, echo=True)

@task
def add_to_firewall(ctx):
    pass

def ls(ctx, pod):
    ls = """
        kubectl get po -o=name | awk -F '/' '{print $2}' | grep "%s"
    """ % pod
    return ctx.run(ls, echo=False, hide=True).stdout.split()

@task
def bash(ctx, pod):
    pods = ls(ctx, pod)
    if len(pods) > 1:
        raise "Too many pods"
    else:
        ctx.run("kubectl exec -it %s /bin/bash" % pods[0], echo=True, pty=True)

@task
def logs(ctx, pod):
    pods = ls(ctx, pod)
    if len(pods) > 1:
        raise "Too many pods"
    else:
        ctx.run("kubectl logs %s" % pods[0], echo=True, pty=True)
