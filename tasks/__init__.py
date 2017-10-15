from invoke import Collection        
 
from . import (
    gce,
    helm,
    k8s,
    main
)

ns = Collection.from_module(main)
ns.add_collection(gce)
ns.add_collection(k8s)
ns.add_collection(helm)
