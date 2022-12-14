
export default class RequestBuilder {

    static PREFIX = "http://localhost:8000/";
    static asset = "stock/";
    static EQ = "=";
    static AMP = "&";
    static QM = "?";
  
    static elements = {
          symbol : "symbol",
          interval : "interval",
          startDate : "start_date",
          endDate : "end_date"
    }

    static changeDateFormat(date){// to YYYY-MM-DD
        const offset = date.getTimezoneOffset()
        date = new Date(date.getTime() - (offset*60*1000))
        return date.toISOString().split("T")[0]
    }
  
    static buildStockRequest(symbol, interval, startDate, endDate){
		var request = [];
	
		request.push(
			RequestBuilder.PREFIX, RequestBuilder.asset, RequestBuilder.QM,
			RequestBuilder.elements.symbol, RequestBuilder.EQ, symbol, RequestBuilder.AMP,
			RequestBuilder.elements.interval, RequestBuilder.EQ, interval, RequestBuilder.AMP,
			RequestBuilder.elements.startDate, RequestBuilder.EQ, this.changeDateFormat(startDate), RequestBuilder.AMP,
			RequestBuilder.elements.endDate, RequestBuilder.EQ, this.changeDateFormat(endDate),
		);

		return request.join("");
    }

    static buildTwitterUserRequest(name, startDate, endDate){
        var requestUrl = [];
    
        requestUrl.push(
			RequestBuilder.PREFIX, RequestBuilder.asset, RequestBuilder.QM,
			RequestBuilder.elements.name, RequestBuilder.EQ, name, RequestBuilder.AMP,
			RequestBuilder.elements.startDate, RequestBuilder.EQ, this.changeDateFormat(startDate), RequestBuilder.AMP,
			RequestBuilder.elements.endDate, RequestBuilder.EQ, this.changeDateFormat(endDate),
        );

        return requestUrl.join("")
    }
  }
