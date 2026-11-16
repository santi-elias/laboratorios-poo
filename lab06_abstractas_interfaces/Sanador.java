/**
 * Interfaz Sanador - Define la capacidad de curar aliados.
 * Los personajes que implementen esta interfaz pueden restaurar
 * puntos de vida a otros personajes.
 */
public interface Sanador {
    void curarAliado(Personaje aliado);
    int getPoderCuracion();
}
