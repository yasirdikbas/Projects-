import java.nio.file.Path;
import java.nio.file.Paths;

public class ConfigPathUtil {
    public static String getConfigPath() {
        Path currentRelativePath = Paths.get("");
        String currentWorking = currentRelativePath.toAbsolutePath().toString();
        return currentWorking + "\\src\\test\\java\\config\\";
    }
}