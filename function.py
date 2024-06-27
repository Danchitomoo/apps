from models import db,  Sell, Sell_Detail

def db_update(temp):
    #Sellへの反映
    try:
        last_sell = db.session.query(Sell).order_by(Sell.sell_id.desc()).first()
        last_sell_sum = last_sell.sell_sum
        last_gain_sum = last_sell.gain_sum
    except:
        last_sell_sum = 0
        last_gain_sum = 0
    sell = Sell()
    sell.sell_sum = last_sell_sum + temp.sell_sum_value
    sell.gain_sum = last_gain_sum + temp.gain_sum_value
    db.session.add(sell)
    db.session.commit()
    #Sell_Detailへの反映
    now_sell = db.session.query(Sell).order_by(Sell.sell_id.desc()).first()
    sell_id = now_sell.sell_id
    for merchant in temp.merchants_sell_name:
        sell_detail = Sell_Detail()
        sell_detail.sell_id = sell_id
        sell_detail.mer_id = merchant
        sell_detail.quantity = temp.merchants_sell_num[merchant]
        db.session.add(sell_detail)
        db.session.commit()


    
    
    
    