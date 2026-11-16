/**
 * Interfaz Hechicero - Define la capacidad de usar magia.
 * Los personajes que implementen esta interfaz pueden lanzar hechizos
 * y tienen un recurso de maná.
 */
public interface Hechicero {
    void lanzarHechizo();
    int getMana();
}
