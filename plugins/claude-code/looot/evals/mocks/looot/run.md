---
expect:
  endpointId: string
  idempotencyKey: string
---

{"tool":"run","data":{"runId":"run_eval0001","idempotencyKey":"{{input.idempotencyKey}}","endpointId":"builtwith-free1-api-json","status":"completed","outcome":"hit","actualCost":0,"result":{"domain":"linear.app","groups":[{"name":"analytics","live":5,"dead":17},{"name":"javascript","live":10,"dead":32},{"name":"hosting","live":5,"dead":10},{"name":"payment","live":4,"dead":4}]}}}
