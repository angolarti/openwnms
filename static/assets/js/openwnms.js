 function request(method = 'GET', url, async, body, fn) {
     console.log('loading...')
     let xnlRequest = new XMLHttpRequest()
     xnlRequest.onreadystatechange = () => {
         if (xnlRequest.readyState === 4) {
             console.log('Finish...')
             fn(JSON.parse(xnlRequest.responseText))
             return JSON.parse(xnlRequest.responseText)
         }
     }
     xnlRequest.open(method, url, async)
     xnlRequest.setRequestHeader("Content-Type", "application/json")
     xnlRequest.send(JSON.stringify(body))
 }
 
 const terminalsStatus = {
     up: 0,
     down: 0
 }

 function pingAndShowData (addr) {
     return request('POST', 'http://localhost:5000/ping', true, {ip: addr}, (response) => {
         let status = document.getElementById(addr)
         if (response.online) {
             terminalsStatus.up += 1
             console.log('UP: ', terminalsStatus.up)
             document.getElementById('up').innerHTML = `Activos: ${terminalsStatus.up}`
             status.classList.add('link-up')
         } else {
             terminalsStatus.down += 1
             document.getElementById('down').innerHTML = `Activos: ${terminalsStatus.down}`
             status.classList.add('link-down')
         }
         var context = document.getElementById('terminais_actives').getContext('2d');
         var grafico = new Chart(context, {
             type: 'doughnut',
             data: {
                 datasets: [{
                     backgroundColor: ['green', 'red'],
                     data: [terminalsStatus.up, terminalsStatus.down] // values by month
                 }]
             }
         })
     })
 }

 function getDevicesIpOnly(tableId) {
     let table = document.getElementById(tableId)
     devicesIp = []
     for (let i = 1; i < table.rows.length; i++) {
         devicesIp.push(table.rows[i].cells[2].firstChild.textContent)
     }
     return devicesIp
 }

 function verifyDeviceOnline () {
     let allDevices = getDevicesIpOnly('table_device')
     for (let device of allDevices) {
         pingAndShowData(device)
     }
 }

 verifyDeviceOnline()

 const buttonRescan = document.getElementById('btnRescan')
 buttonRescan.addEventListener('click', () => {
     // spinner-border spinner-border-sm
     let span = buttonRescan.childNodes[1]
     span.classList.add('spinner-border', 'spinner-border-sm')
     console.log('Starting rescan...')
     return request('POST', 'http://localhost:5000/rescan', true, {}, (response) => {
         alert('Rescan terminado com sucesso')
         span.classList.remove('spinner-border', 'spinner-border-sm')
     })
 })