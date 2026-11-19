
package com.leafvision.config;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public final class DatabaseConnection {

    private DatabaseConnection() {
    }

    public static Connection getConnection() throws SQLException {

        String url = System.getenv("LEAFVISION_DB_URL");
        String user = System.getenv("LEAFVISION_DB_USER");
        String password = System.getenv("LEAFVISION_DB_PASSWORD");

        if (url == null || url.isEmpty()
                || user == null || user.isEmpty()
                || password == null) {

            throw new SQLException(
                "La configuracion de la base de datos esta incompleta."
            );
        }

        return DriverManager.getConnection(url, user, password);
    }
}
