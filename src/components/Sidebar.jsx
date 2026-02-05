function Sidebar({ buildings, selectedBuilding, onSelect }) {
  return (
    <aside className="sidebar">
      <h1>Building Viewer</h1>
      <ul className="building-list">
        {buildings.map((building) => (
          <li
            key={building.id}
            className={`building-item ${selectedBuilding.id === building.id ? 'active' : ''}`}
            onClick={() => onSelect(building)}
          >
            <h3>{building.name}</h3>
            <p>{building.description}</p>
          </li>
        ))}
      </ul>
    </aside>
  )
}

export default Sidebar
