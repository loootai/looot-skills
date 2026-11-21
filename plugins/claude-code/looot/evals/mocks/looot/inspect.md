---
expect:
  endpointId: string
---

{"tool":"inspect","data":{"endpoint":{"id":"{{input.endpointId}}","provider":"BuiltWith","capability":"company.technographics"},"price":{"basis":"perResult","usd":0},"estimatedMaxCost":0,"requiredInputFields":["LOOKUP"],"inputSchema":{"type":"object","properties":{"LOOKUP":{"type":"string","description":"The domain to look up, for example example.com"}},"required":["LOOKUP"]},"run":{"endpointId":"{{input.endpointId}}","input":{"LOOKUP":"<domain>"},"idempotencyKey":"<new key>"}}}
