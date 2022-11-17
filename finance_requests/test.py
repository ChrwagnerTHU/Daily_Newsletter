import finance_request
 
#requester = finance_request.requester("J1AF3SZ0S4184JGT", 'stock_info.json')

# for test usage (2nd time, after data is saved as data.json)
requester = finance_request.requester(config_path='stock_info.json')

# get data and save it as data.json
#data = requester.getDataDaily()

# plot data and save as png with userid
requester.plotCourse("steinie")

# get balance
requester.plotStockBalance("steinie")
