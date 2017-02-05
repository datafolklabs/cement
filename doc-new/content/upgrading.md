---
weight: 99
title: Upgrading
---

# Upgrading

This section outlines any information and changes that might need to be made
in order to update your application built on previous versions of Cement.

## 2.8.x to 2.9.x

Cement 2.9 introduces a few incompatible changes from the previous 2.8 stable
release, as noted in the :ref:`ChangeLog <changelog>`.

### Deprecated: cement.core.interface.list()

This function should no longer be used in favor of 
`CementApp.handler.list_types()`.  It will continue to work throughout 
Cement 2.x, however is not compatible if 
`CementApp.Meta.use_backend_globals == False`.

Related: 

 * [Issue #366](https://github.com/datafolklabs/cement/issues/366)
 * [Issue #376](https://github.com/datafolklabs/cement/issues/376)


