import java.util.Scanner;

public class SimplifyExpression {
public static void main(String[] args) {
Scanner sc = new Scanner(System.in);
int a = sc.nextInt();
int b = sc.nextInt();
sc.close();

    if (a == 0) {
        System.out.println(b);
    } else if (b == 0) {
        if (a == 1) {
            System.out.println("x");
        } else if (a == -1) {
            System.out.println("-x");
        } else {
            System.out.println(a + "x");
        }
    } else {
        String sign = (b > 0) ? "+" : "-";
        b = Math.abs(b);
        if (a == 1) {
            System.out.println("x" + sign + b);
        } else if (a == -1) {
            System.out.println("-x" + sign + b);
        } else {
            System.out.println(a + "x" + sign + b);
        }
    }
}

}
