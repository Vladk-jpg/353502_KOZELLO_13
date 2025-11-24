const address = 'https://data-api.coindesk.com/index/cc/v1/latest/tick?market=cadli&instruments=BTC-USD,ETH-USD&apply_mapping=true';

document.addEventListener('DOMContentLoaded', async () => {
  const element = document.getElementById('bitcoin-price');
  const token = element.getAttribute('data-api-key');
  await fetch(address, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  }).then((response) => {
    if (!response.ok) {
      throw new Error('Couldn\'t get result from api');
    }
    return response.json();
  })
    .then((data) => {
      console.log(data);
      const element = document.getElementById('bitcoin-price');
      const p = document.createElement('p');
      let price = data.Data['BTC-USD'].VALUE;
      price = parseFloat(price).toFixed(2);
      p.innerText = `Стоимость биткоина: ${price}$`;
      element.appendChild(p);
    })
    .catch((error) => console.error('Error:', error));;
})