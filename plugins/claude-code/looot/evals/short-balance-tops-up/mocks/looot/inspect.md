---
expect:
  endpointId: string
---

{"tool":"inspect","data":{"endpoint":{"id":"{{input.endpointId}}","provider":"Kitt AI","capability":"people.email.find"},"price":{"basis":"perCall","usd":0.005},"estimatedMaxCost":0.005,"requiredInputFields":["first_name","last_name","domain"],"inputSchema":{"type":"object","properties":{"first_name":{"type":"string"},"last_name":{"type":"string"},"domain":{"type":"string","description":"Company domain, for example acme.com"}},"required":["first_name","last_name","domain"]},"run":{"endpointId":"{{input.endpointId}}","input":{"first_name":"<first name>","last_name":"<last name>","domain":"<domain>"},"idempotencyKey":"<new key>"}}}
