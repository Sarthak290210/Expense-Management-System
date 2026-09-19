from Backend import db_helper

def test_fetch_expenses_by_date_02_aug():
    expenses = db_helper.fetch_expenses_by_date('2024-09-30')
    
    assert len(expenses) == 6
    assert expenses[0]['amount'] == 1000
    assert expenses[0]['category'] == 'Rent'
    assert expenses[1]["amount"] == 250
    assert expenses[1]["category"] == 'Food'

def test_fetch_expenses_summary_01_sep_to_30_sep():
    summary = db_helper.fetch_expenses_summary('2024-09-01', '2024-09-30')
    
    assert len(summary) == 5
    assert summary[0]['Category'] == 'Rent'
    assert summary[0]['total_amount'] == 2550
    assert summary[1]['Category'] == 'Food'
    assert summary[1]['total_amount'] == 1175
    assert summary[4]['Category'] == 'Other'
    assert summary[3]['total_amount'] == 265
