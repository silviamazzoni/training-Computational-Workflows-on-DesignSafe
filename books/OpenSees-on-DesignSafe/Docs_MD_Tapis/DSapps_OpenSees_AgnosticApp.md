# DesignSafe Agnostic App on DesignSafe

***The Agnostic App: A Unified Execution Model***

To address scalability, sustainability, and flexibility, DesignSafe introduced the **agnostic Tapis app**.

Instead of being tied to a single application, the agnostic app provides a **general execution framework** capable of running:

* OpenSees (serial, MP, SP)
* OpenSeesPy
* Pure Python workflows
* Parametric sweeps
* Multi-step pipelines
* Custom executables

All of the legacy OpenSees apps are conceptually **special cases** of this model.

---

## A Trade-Off Worth Making

The agnostic app **does require a bit more understanding from the user**, because it exposes:

* execution modes
* resource choices
* command structure
* file-staging behavior

But in return, it provides:

* **far more functionality**
* **one consistent interface**
* **faster feature development**
* **long-term maintainability**
* **the ability to support non-OpenSees workflows**

This is a deliberate shift:

> from *“one app per use case”*
> to *“one execution model that scales”*

