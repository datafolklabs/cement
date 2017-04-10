---
weight: 10
title: API
---

# Innleiing

Velkomen skal du vere til Kittn API! Du kan bruke vårt API til å kalle våre Kittn endepunkt. Her kan du hente ut ymse informasjon om kattar, kattungar og ulike rasar frå vår database.

Her finn du kodedøme i Shell, Ruby, Python og Go! Du ser desse døma i det mørke feltet til høgre på skjermen -- og du kan byta programmeringsspråk ved å klikke på menyen oppe til høgre.

**Denne API-dokumentasjonen vart laga med  [DocuAPI](https://github.com/bep/docuapi/),  eit tema for den statiske nettstadsmakaren [Hugo](http://gohugo.io/).** 

# Autentisering

> For å autentisere ein brukar, bruk denne koden:

```go
package main

import "github.com/bep/kittn/auth"

func main() {
	api := auth.Authorize("meowmeowmeow")

	// Just to make it compile
	_ = api
}
```

```ruby
require 'kittn'

api = Kittn::APIClient.authorize!('meowmeowmeow')
```

```python
import kittn

api = kittn.authorize('meowmeowmeow')
```

```shell
# With shell, you can just pass the correct header with each request
curl "api_endpoint_here"
  -H "Authorization: meowmeowmeow"
```

```javascript
const kittn = require('kittn');

let api = kittn.authorize('meowmeowmeow');
```

> Gjer vel og erstatt `meowmeowmeow` med din eigen API-nøkkel.

Kittn tek i bruk API-nøklar for å gi tilgang til APIet. Du kan kan registrere deg for å få ein slik nøkkel på vår  [utviklarportal](http://example.com/developers).

Kittn forventar at API-nøkkelen er med i alle API-førespurnader til serveren i ein header som ser slik ut:

`Authorization: meowmeowmeow`

<aside class="notice">
Merk:  Du må erstatte <code>meowmeowmeow</code> med din personlege nøkkel.</aside>

# Kattungar

## Hent alle kattungane

```go
package main

import "github.com/bep/kittn/auth"

func main() {
	api := auth.Authorize("meowmeowmeow")

	_ = api.GetKittens()
}
```

```ruby
require 'kittn'

api = Kittn::APIClient.authorize!('meowmeowmeow')
api.kittens.get
```

```python
import kittn

api = kittn.authorize('meowmeowmeow')
api.kittens.get()
```

```shell
curl "http://example.com/api/kittens"
  -H "Authorization: meowmeowmeow"
```

```javascript
const kittn = require('kittn');

let api = kittn.authorize('meowmeowmeow');
let kittens = api.kittens.get();
```

> Programmet over gir ein JSON-struktur som ser slik ut:

```json
[
  {
    "id": 1,
    "name": "Fluffums",
    "breed": "calico",
    "fluffiness": 6,
    "cuteness": 7
  },
  {
    "id": 2,
    "name": "Max",
    "breed": "unknown",
    "fluffiness": 5,
    "cuteness": 10
  }
]
```

Dette endepunktet leverer alle kattungar.

### HTTP-førespurnad

`GET http://example.com/api/kittens`

### Query-parametrar

Parameter | Standardverdi | Skildring
--------- | ------- | -----------
include_cats | false | Set til true for å få alle kattar.
available | true | Set til false for å ta med kattar som allereie er blitt adoptert vekk.

<aside class="success">
Hugs — ein lukkeleg kattunge er ein autentisert kattunge!
</aside>

## Hent éin kattunge

```go
package main

import "github.com/bep/kittn/auth"

func main() {
	api := auth.Authorize("meowmeowmeow")

	_ = api.GetKitten(2)
}
```

```ruby
require 'kittn'

api = Kittn::APIClient.authorize!('meowmeowmeow')
api.kittens.get(2)
```

```python
import kittn

api = kittn.authorize('meowmeowmeow')
api.kittens.get(2)
```

```shell
curl "http://example.com/api/kittens/2"
  -H "Authorization: meowmeowmeow"
```

```javascript
const kittn = require('kittn');

let api = kittn.authorize('meowmeowmeow');
let max = api.kittens.get(2);
```

> Programmet over gir ein JSON-struktur som ser slik ut:

```json
{
  "id": 2,
  "name": "Max",
  "breed": "unknown",
  "fluffiness": 5,
  "cuteness": 10
}
```

Dette endepunktet hentar ut éin spesifikk kattunge.

<aside class="warning">Inne i HTML-blokker som denne så kan du ikkje bruke Markdown.  Bruk <code>&lt;code&gt;</code> for å markere kjeldekode.</aside>

### HTTP-førespurnad

`GET http://example.com/kittens/<ID>`

### URL-parametrar

Parameter | Skildring
--------- | -----------
ID | IDen til kattungen du ynskjer å hente

