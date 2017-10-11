from invoke import Collection        
 
from . import (
    main,
    gce,
    helm
)

ns = Collection.from_module(main)
ns.add_collection(gce)
ns.add_collection(helm)
