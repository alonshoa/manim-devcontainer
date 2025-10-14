public class BubbleSort
{
    public static void Main(){
        int[] arr = {12,23,34,45,56,78,65,34,52,12};
        // iteration if i
        for (int i = 0 ; i < arr.Length - 1 ; i++){
            // iteration for j
            for (int j = 0 ; j < arr.Length - 1 - i ; j++){
                // check if we need to swap
                if (arr[j] > arr[j+1]){
                    // do the swap
                    int tmp = arr[j];
                    arr[j] = arr[j+1];
                    arr[j+1]  tmp;
                }
            }
        }
    }
}
