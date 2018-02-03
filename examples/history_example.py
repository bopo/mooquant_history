from mooquant_history.history import History

his = History(symbol='000001')
ma5 = his['000001'].MA(5)

print(ma5)