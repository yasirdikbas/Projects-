#ifndef CALCULATOR_H
#define CALCULATOR_H

#include <QMainWindow>
#include <QQueue>

QT_BEGIN_NAMESPACE
namespace Ui { class Calculator; }
QT_END_NAMESPACE

class Calculator : public QMainWindow
{
    Q_OBJECT

public:
    Calculator(QWidget *parent = nullptr);
    ~Calculator();

private:
    enum class Type { Number, ArithmeticOperator};
    struct QueueEntry {
        QString value;
        Type type;
    };
private:
    Ui::Calculator *ui;
    QQueue<QueueEntry> queue;   // Holds all the entries on the display for later on calculations
    bool clearDisplay = false;

private slots:
    // Called when a number button [ 0 : F ] or an arithmetic operator button [ +, - ] is pressed
    void numberOrOperatorPressed();
    // Called when equal button [ = ] is pressed
    void equalPressed();
    // Called when clear button [ Cls ] is pressed
    void clearPressed();
};
#endif // CALCULATOR_H
