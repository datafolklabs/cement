---
weight: 20
title: Feil

---

# Feil

<aside class="notice">Denne seksjonen om feil er lagra i éiga fil, errors.md. DocuAPI let deg dele dokumentasjonen inn i så mange filer som du måtte ynskje. Filene blir henta inn i standard Hugo-rekkjefølgje. Den lettaste måten å styre denne rekkjefølgja er å sette vekt på kvar side, t.d. `weight=10` Sidene med lågast vekt blir vist først.</aside>

Kittn-APIet tek i bruk følgjande feilkodar:

Feilkode | Forklaring
---------- | -------
400 | Bad Request -- Din førespurnad har forbetringspotensiale
401 | Unauthorized -- Feil API-nøkkel
403 | Forbidden -- Denne kattungen er berre tilgjengeleg for administratorar
404 | Not Found -- Denne kattungen vart ikkje funnen
405 | Method Not Allowed -- Du prøvde å få tak i kattungen på ein snodig og ulovleg måte
406 | Not Acceptable -- Du bad om eit format som ikkje er  JSON
410 | Gone -- Kattungen har rømt frå serveren.
418 | I'm a teapot
429 | Too Many Requests -- Du spør om for mange kattungar, ta det med ro!
500 | Internal Server Error -- Me har eit problem med serveren. Prøv igjen seinare.
503 | Service Unavailable -- Me er nede for vedlikehald. Prøv igjen seinare.

