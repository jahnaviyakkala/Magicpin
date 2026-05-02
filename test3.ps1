$merchantBody = @"
{
  "scope": "merchant",
  "context_id": "m_003",
  "version": 1,
  "payload": {
    "name": "Struggling Restaurant",
    "category": "restaurant",
    "rating": 3.2,
    "listing_score": 80,
    "response_rate": 0.9,
    "last_active_days": 2,
    "offers": 1
  }
}
"@

$triggerBody = @"
{
  "scope": "trigger",
  "context_id": "trg_003",
  "version": 1,
  "payload": {
    "type": "spike",
    "value": "Search"
  }
}
"@

$tickBody = @"
{
  "now": "2026-04-29T12:00:00Z",
  "available_triggers": ["trg_003"]
}
"@

Write-Host "Adding low rating merchant (m_003)..."
Invoke-RestMethod -Uri "http://127.0.0.1:8000/v1/context" -Method Post -ContentType "application/json" -Body $merchantBody

Write-Host "Adding spike trigger (trg_003)..."
Invoke-RestMethod -Uri "http://127.0.0.1:8000/v1/context" -Method Post -ContentType "application/json" -Body $triggerBody

Write-Host "Calling /tick..."
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/v1/tick" -Method Post -ContentType "application/json" -Body $tickBody

Write-Host "TICK RESPONSE:"
$response | ConvertTo-Json -Depth 5
