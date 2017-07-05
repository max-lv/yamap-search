


function switchBlocks(showResult, errorText) {
  errorText = errorText ? errorText : "";
  if(showResult) {
    document.querySelector('.result-block').style = "display:block;";
    document.querySelector('.error-block').style = "display:none;";
  } else {
    document.querySelector('#info2').innerText = errorText;
    document.querySelector('.result-block').style = "display:none;";
    document.querySelector('.error-block').style = "display:block;";
  }
}

switchBlocks(false);

document.querySelector('button').addEventListener('click', function(e) {
  let input = document.querySelector('input'),
      city = input.value;

  fetch('http://127.0.0.1:5000/api/?city=' + city)
    .then((req) => (req.json()))
    .then((json)=> {
      if (!json.success) {
        switchBlocks( false, 'Во время поиска возникла ошибка!');
        return;
      }

      // hide table if we found nothing
      if(json.total==0) {
        switchBlocks( false, 'Ниодной заправки не было найдено.');
      } else {
        // display table
        switchBlocks(true);

        // counter info above table
        document.querySelector('#info').innerText = 'Всего найдено заправок: ' + json.total;

        // generate table
        table_content = "";
        for(var i=0;i<json.data.length;i++) {
          table_content += '<tr><td>' +
            json.data[i].id +
            '</td><td>' +
            json.data[i].coordinates[0] +
            '</td><td>' +
            json.data[i].coordinates[1] +
            '</td><td>' +
            json.data[i].address +
            '</td></tr>';
        }

        document.querySelector('table tbody').innerHTML = table_content;

        document.querySelector('#download').setAttribute('href', '/csv/' + json.file_id);
      }
    });
});