package com.gestaoconfeitaria.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseConnection {
    // Configurações para o banco PostgreSQL
    private static final String URL = "jdbc:postgresql://localhost:5432/gestaoconfeitaria";
    private static final String USER = "postgres";
    private static final String PASSWORD = "@NaVaJo68#PostGre#";

    // Método para conectar ao banco
    public static Connection connect() throws SQLException {
        try {
            return DriverManager.getConnection(URL, USER, PASSWORD);
        } catch (SQLException e) {
            System.err.println("Erro ao conectar ao banco: " + e.getMessage());
            throw e;
        }
    }
}