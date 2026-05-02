$merchantBody = @"
{
  "scope": "merchant",
  "context_id": "m_002",
  "version": 1,
  "payload": {
    "name": "Healthy Salon",
    "category": "salon",
    "rating": 4.8,
    "listing_score": 95,
    "response_rate": 0.98,
    "last_active_days": 1,
    "offers": 0
  }
}
"@

$triggerBody = @"
{
  "scope": "trigger",
  "context_id": "trg_002",
  "version": 1,
  "payload": {
    "type": "festival",
    "value": "Diwali"
  }
}
"@

$tickBody = @"
{
  "now": "2026-04-29T11:00:00Z",
  "available_triggers": ["trg_002"]
}
"@

Write-Host "Adding healthy merchant (m_002)..."
Invoke-RestMethod -Uri "http://127.0.0.1:8000/v1/context" -Method Post -ContentType "application/json" -Body $merchantBody

Write-Host "Adding festival trigger (trg_002)..."
Invoke-RestMethod -Uri "http://127.0.0.1:8000/v1/context" -Method Post -ContentType "application/json" -Body $triggerBody

Write-Host "Calling /tick for healthy merchant..."
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/v1/tick" -Method Post -ContentType "application/json" -Body $tickBody

Write-Host "TICK RESPONSE:"
$response | ConvertTo-Json -Depth 5
