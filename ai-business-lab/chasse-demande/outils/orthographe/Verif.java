import org.languagetool.JLanguageTool;
import org.languagetool.Languages;
import org.languagetool.rules.RuleMatch;
import java.nio.file.*;
import java.util.*;
public class Verif {
  public static void main(String[] a) throws Exception {
    JLanguageTool lt = new JLanguageTool(Languages.getLanguageForShortCode("fr"));
    String t = Files.readString(Path.of(a[0]));
    for (RuleMatch m : lt.check(t)) {
      int s = Math.max(0, m.getFromPos() - 30), e = Math.min(t.length(), m.getToPos() + 30);
      System.out.println(m.getRule().getId() + "\t" + t.substring(m.getFromPos(), m.getToPos()).replace("\n"," ") + "\t" + String.join("|", m.getSuggestedReplacements().subList(0, Math.min(3, m.getSuggestedReplacements().size()))) + "\t" + t.substring(s, e).replace("\n", " "));
    }
  }
}
