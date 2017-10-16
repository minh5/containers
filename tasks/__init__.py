from invoke import Collection        
 
from . import (
    gce,
    helm,
    k,
    main
)

ns = Collection.from_module(main)
ns.add_collection(gce)
ns.add_collection(k)
ns.add_collection(helm)
