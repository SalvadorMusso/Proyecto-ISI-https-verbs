# Proyecto-ISI-https-verbs
primer proyecto de ISI l sobre http en python


// Invoke-RestMethod -Uri http://localhost:9292/tasks -Method Post -ContentType "application/json" -Body '{"tarea": "Lavar los platos", "estado": false}'

// Invoke-RestMethod -Uri http://localhost:9292/tasks/1 -Method Patch -ContentType "application/json" -Body '{"estado": true}'




Invoke-RestMethod -Uri "http://localhost:9292/tasks" -Method Get

Invoke-RestMethod -Uri "http://localhost:9292/tasks" -Method Post -ContentType "application/json" -Body '{"title": "Estudiar HTTP", "done": false}'

Invoke-RestMethod -Uri "http://localhost:9292/tasks/1" -Method Get

Invoke-RestMethod -Uri "http://localhost:9292/tasks/1" -Method Patch -ContentType "application/json" -Body '{"done": true}'

Invoke-RestMethod -Uri "http://localhost:9292/tasks/1" -Method Delete

try {
    Invoke-RestMethod -Uri "http://localhost:9292/tasks/999" -Method Get
} catch {
    $_.Exception.Response.StatusCode.value__
}