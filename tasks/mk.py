from invoke import task

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