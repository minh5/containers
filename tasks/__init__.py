from invoke import Collection        
 
from . import (
    gce,
    helm,
    k,
    main,
    mk
)

ns = Collection.from_module(main)
ns.add_collection(gce)
ns.add_collection(k)
ns.add_collection(helm)
ns.add_collection(mk)
