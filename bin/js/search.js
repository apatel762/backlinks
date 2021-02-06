var idx;

function populateLunrIndex(json) {
    return lunr(function(){
        this.ref('href')
        this.field("title", {
            boost: 10
        });

        json.forEach(function(element) {
            try {
                this.add(element)
            } catch (e) {
                // no-op; swallow exception
            }
        }, this);
    });
}

fetch('/js/index.json')
    .then(response => response.json())
    .then(json => idx = populateLunrIndex(json))
    .catch(err => alert('something went wrong getting the index.json' + err));