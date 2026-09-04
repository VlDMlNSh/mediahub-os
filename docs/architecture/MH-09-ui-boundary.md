# MH-09 — UI Boundary

**Status:** PROPOSED

## Rule
Presentation is a consumer surface. It may read authorized read models and submit explicit requests/proposals, but it cannot mutate canonical state directly.

## Allowed
- bounded authorized reads;
- user intent and local drafts;
- explicit command/request/proposal creation;
- result and error presentation;
- bounded security/audit information;
- presentation cache/session state.

## Forbidden
- direct State Authority access;
- raw transaction handles;
- direct persistence/database access;
- direct device mutation;
- arbitrary shell/subprocess;
- unrestricted filesystem/network;
- plugin execution authority;
- capability self-grant or escalation.

UI visibility, disabled controls, routes, deep links and local state are not authorization controls.

## Boundary test
Every mutation path must be demonstrable as Presentation → explicit contract → authorization/policy → Consumer Boundary → canonical authority/controlled subsystem.
