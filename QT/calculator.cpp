#include "calculator.h"
#include "ui_calculator.h"

Calculator::Calculator(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::Calculator)
{
    ui->setupUi(this);

    QString numberAndOperatorsButtonsText[18] = { "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "Plus", "Minus" };
    QPushButton* numberAndOperatorsButtons[18];  // [ 0: F ] && [ '+', '-']

    /*
     * Loop all over the numbers and operators [+,-] button to get a reference to them by using their name ( the name was given in "calculator.ui" ) .
     * So we can connect their release signal (when the button is released) to the numberOrOperatorPressed() slot ( call this function when button is released )
    */
    for(int i = 0; i<18; i++)
    {
        QString buttonName = "Button" + QString(numberAndOperatorsButtonsText[i]);      // Set the button name in the same format as in "calculator.ui"

        // Get the push button by it's name (the name that was given in calculator.ui)
        numberAndOperatorsButtons[i] = Calculator::findChild<QPushButton*>(buttonName);

        // Call the function numberOrOperatorPressed() whenever a number or operator button is released
        connect(numberAndOperatorsButtons[i], SIGNAL(released()), this, SLOT(numberOrOperatorPressed()));
    }

    // Call the function equalPressed() when equal button is released
    connect(Calculator::findChild<QPushButton*>("ButtonEqual"), SIGNAL(released()), this, SLOT(equalPressed()));

    // Call the function numberPressed() when clear button is released
    connect(Calculator::findChild<QPushButton*>("ButtonClear"), SIGNAL(released()), this, SLOT(clearPressed()));
}

Calculator::~Calculator()
{
    delete ui;
}

QString Calculate(QString& firstOperant, QString& secondOperant, QString& arithmeticOperator)
{
    /*
     *  Calculates the result of the last operand and previous operand with the given arithmetic operator
    */

    int result = 0;

    if(arithmeticOperator == "+")   // Addition
        result = firstOperant.toInt(nullptr, 16) + secondOperant.toInt(nullptr, 16); // Convert the values to base16 (hexadecimal);
    else if(arithmeticOperator == "-")  // Subtraction
        result = firstOperant.toInt(nullptr, 16) - secondOperant.toInt(nullptr, 16); // Convert the values to base16 (hexadecimal);

    // Clear inputs (Note: the inputs are passed by reference)
    firstOperant = "";
    secondOperant = "";
    arithmeticOperator = "";

    if(result < 0)
        return ("-" + QString::number(result * -1, 16).toUpper() );
    return (QString::number(result, 16)).toUpper();   // Return the result in Hexadecimal format and uppercase
}

void Calculator::numberOrOperatorPressed()
{
    /*
     * Called when a number [ 0 : F ] or an arithmetic operator [ +, - ] is pressed
     * This function stores the numbers and arithmetic operator in a queue, to be calculated when the equal button is pressed ( Handled in equalPressed() )
    */

    // Check if display has to be cleared first ( there is old calculations on the display )
    if(clearDisplay)
    {
        // Clear display
        ui->Display->setText("");
        clearDisplay = false;
    }

    // Get the pressed button from the signal
    QPushButton* pressedButton = reinterpret_cast<QPushButton*>(sender());  // Cast QObject* ( the return value from sender() ) to QPushButton*
    // Get pressed button value
    QString buttonValue = pressedButton->text();



    // Get the entry type [ Number, ArithmeticOperator ]. ( Is it a Number button or ArithmeticOperator button )
    Type entryType = Type::ArithmeticOperator;
    if(buttonValue != "+" && buttonValue != "-")   // If it is not "+" or "-" button then it must be a number button
    {
        entryType = Type::Number;
    }

    // Handle when multiple arithmetic operators are entered directly after another  @ex: ++++, ----
    if(!queue.isEmpty())
    {
        auto queueList = queue;           // Convert the queue to list to get the last entry
        auto& lastQueueEntry = queueList.last();   // Last entry

        // If the last entry is either '+' or '-', exit (return) the funtion
        if(entryType == Type::ArithmeticOperator && (lastQueueEntry.value == "+" || lastQueueEntry.value == "-"))
            return;
    }
    // Handles the invalid case @ex: -|+CF+17B
    else  // When queue is empty
    {
         if(entryType == Type::ArithmeticOperator)
             return;
    }

    // Add the pressed button value to the queue
    QueueEntry entry = { buttonValue, entryType };
    queue.enqueue(entry);

    // Get current display value
    QString displayValue = ui->Display->text();
    // Append the pressed button value to current display value
    displayValue += buttonValue;

    // Set new display value to UI
    ui->Display->setText(displayValue);

}
void Calculator::equalPressed()
{
    /*
     * Called when the equal button [ = ] is pressed
    */

    // Initialization
    QString firstOperant = "0";
    QString arithmeticOperator = "+";
    QString longestContiguousNumber = "";
    QString result = "";

    // Loop over all the entries from the queue
    while (!queue.isEmpty())
    {
        // Get first entry from the queue
        QueueEntry entry = queue.dequeue();
        QString entryValue = entry.value;
        Type entryType = entry.type;

        if(entryType == Type::Number)
        {
            // Append the single digits, until we get the full operant
            longestContiguousNumber += entryValue;
        }
        else if (entryType == Type::ArithmeticOperator)
        {
            if(firstOperant == "")  // If we don't have a first operant yet and we encountered an ArithmeticOperator [ +, - ]
            {
                firstOperant = longestContiguousNumber;
                longestContiguousNumber = "";
            }
            else  // We have all there element to make a calculation ( First operant, Second operant (longestContiguousNumber), arithmeticOperator )
            {
                result = Calculate(firstOperant, longestContiguousNumber, arithmeticOperator);
                ui->Display->setText(result);    // Set the result to the display
                firstOperant = result;  // Set the result to be the new first operant for further calculations
            }
            arithmeticOperator = entryValue;
        }
    }

     // We have all there element to make a calculation ( First operant, Second operant (longestContiguousNumber), arithmeticOperator )
    if(firstOperant!= "" && longestContiguousNumber != "" && arithmeticOperator != "")
    {
        result = Calculate(firstOperant, longestContiguousNumber, arithmeticOperator);
        ui->Display->setText(result);   // Set the result to the display
        firstOperant = result;       // Set the result to be the new first operant for further calculations
        clearDisplay = true;
    }

}

void Calculator::clearPressed()
{
    /*
     * Called when clear button [ Cls ] is pressed
    */

    // Clear display
    ui->Display->setText("");

    // Clear queue
    if(!queue.isEmpty())
    {
        queue.clear();
    }
}
