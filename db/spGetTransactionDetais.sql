ALTER Procedure spGetTransactionDetais 
(
    @TransactionID VARCHAR(100)
)
AS
BEGIN
-- Get a list of tables and views in the current database
SELECT transaction_id, user_id, merchant, amount, currency, payment_method, payment_gateway
transaction_date, status 
FROM dbo.Transactions where transaction_id = @TransactionID

END

GO

