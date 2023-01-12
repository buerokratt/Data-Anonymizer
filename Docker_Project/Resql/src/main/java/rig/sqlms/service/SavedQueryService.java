package rig.sqlms.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Service;
import rig.sqlms.exception.InvalidDirectoryException;
import rig.sqlms.exception.ResqlRuntimeException;
import rig.sqlms.model.SavedQuery;

import java.io.File;
import java.util.HashMap;
import java.util.Map;

@Service
@Slf4j
public class SavedQueryService {
    private final Map<String, SavedQuery> savedQueries = new HashMap<>();

    public SavedQueryService(@Value("${sqlms.saved-queries-dir}") String savedQueriesDir) {
        log.info("Initializing SavedQueryService");
        loadQueries(getConfigDir(savedQueriesDir).listFiles());
    }

    private void loadQueries(File[] filesList) {
        try {
            if (filesList != null) {
                for (File file : filesList) {
                    if (file.isDirectory()) {
                        loadQueries(file.listFiles());
                    } else {
                        try {
                            savedQueries.put(getQueryName(file), SavedQuery.of(file.getAbsolutePath()));
                        } catch (Throwable t) {
                            log.error("Failed parsing saved query file {}", file.getName(), t);
                        }
                    }
                }
            }
        } catch (Exception e) {
            log.error("Failed loading configuration service", e);
        }
    }

    private String getQueryName(File file) {
        return file.getName().substring(0, file.getName().lastIndexOf(".")).toLowerCase();
    }

    @NonNull
    public SavedQuery get(String name) {
        SavedQuery query = savedQueries.get(name.trim().toLowerCase());

        if (query == null) {
            throw new ResqlRuntimeException("Saved query '%s' does not exist".formatted(name));
        }

        return query;
    }

    private File getConfigDir(String path) {
        File configDir;
        if (path == null || path.isEmpty())
            throw new InvalidDirectoryException("Saved configuration directory seems to empty");

        configDir = new File(path);
        if (!configDir.exists() && !configDir.isDirectory())
            throw new InvalidDirectoryException("Saved configuration directory missing or not a directory");

        return configDir;
    }
}
