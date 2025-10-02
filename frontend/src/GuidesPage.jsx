import React, { useState } from 'react'
import { DndContext, useDraggable, useDroppable, DragOverlay } from '@dnd-kit/core';

const pilgrims = [
    {pilgrimId: 1, name: 'ali', guideid: 1 , hotel:"Assafa", checkin: '2024-06-01', checkout: '2024-06-10'},
    {pilgrimId: 2, name: 'Bob', guideid: 1, hotel:"Assafa", checkin: '2024-06-01', checkout: '2024-06-10'},
    {pilgrimId: 3, name: 'Charlie', guideid: 1, hotel:"Assafa", checkin: '2024-06-11', checkout: '2024-06-21'},
    {pilgrimId: 4, name: 'David', guideid: 1, hotel:"Assafa", checkin: '2024-06-11', checkout: '2024-06-21'},
    {pilgrimId: 5, name: 'Eve', guideid: 1 , hotel:"Assafa golden", checkin: '2024-06-01', checkout: '2024-06-10'},
    {pilgrimId: 6, name: 'Frank', guideid: 1, hotel:"Assafa golden", checkin: '2024-06-01', checkout: '2024-06-10'},
    {pilgrimId: 7, name: 'Grace', guideid: 1, hotel:"Assafa golden", checkin: '2024-06-01', checkout: '2024-06-10'},
    {pilgrimId: 8, name: 'Heidi', guideid: 1, hotel:"Assafa golden", checkin: '2024-06-01', checkout: '2024-06-10'},
    {pilgrimId: 9, name: 'Ivan', guideid:3, hotel:"Assafa", checkin: '2024-06-01', checkout: '2024-06-10'},
    {pilgrimId: 10, name: 'Judy', guideid: 3, hotel:"Assafa", checkin: '2024-06-01', checkout: '2024-06-10'},
];
const hotels = [
  {
    hotelId: 1,
    name: "Assafa",
    rooms: [
      // Guide 1, 2024-06-01 to 2024-06-10
      { roomId: 101, guideId: 1, checkin: '2024-06-01', checkout: '2024-06-10', capacity: 2, assignedPilgrims: [] },
      { roomId: 102, guideId: 1, checkin: '2024-06-01', checkout: '2024-06-10', capacity: 2, assignedPilgrims: [] },
      // Guide 1, 2024-06-11 to 2024-06-21
      { roomId: 101, guideId: 1, checkin: '2024-06-11', checkout: '2024-06-21', capacity: 2, assignedPilgrims: [] },
      { roomId: 102, guideId: 1, checkin: '2024-06-11', checkout: '2024-06-21', capacity: 2, assignedPilgrims: [] },
      // Guide 3, 2024-06-01 to 2024-06-10
      { roomId: 101, guideId: 3, checkin: '2024-06-01', checkout: '2024-06-10', capacity: 2, assignedPilgrims: [] },
      { roomId: 102, guideId: 3, checkin: '2024-06-01', checkout: '2024-06-10', capacity: 2, assignedPilgrims: [] },
    ]
  },
  {
    hotelId: 2,
    name: "Assafa golden",
    rooms: [
      // Guide 1, 2024-06-01 to 2024-06-10
      { roomId: 201, guideId: 1, checkin: '2024-06-01', checkout: '2024-06-10', capacity: 2, assignedPilgrims: [5, 6] },
      { roomId: 202, guideId: 1, checkin: '2024-06-01', checkout: '2024-06-10', capacity: 2, assignedPilgrims: [7, 8] },
      // Guide 2, 2024-06-01 to 2024-06-10 (example for another guide)
      { roomId: 201, guideId: 2, checkin: '2024-06-01', checkout: '2024-06-10', capacity: 2, assignedPilgrims: [] },
      { roomId: 202, guideId: 2, checkin: '2024-06-01', checkout: '2024-06-10', capacity: 2, assignedPilgrims: [] },
    ]
  }
];
const guideId = parseInt(localStorage.getItem('guideId'));
const guideName = localStorage.getItem('guideName');
function GuidesPage() {
  // Filter pilgrims for this guide
  const myPilgrims = pilgrims.filter((p) => p.guideid === guideId);
  const [selectedHotel, setSelectedHotel] = useState(null);
  const [selectedDate, setSelectedDate] = useState(null);
  // Local state for hotel rooms (so we can update on drag)
  const [localHotels, setLocalHotels] = useState(hotels);
  // For drag overlay
  const [activeDragId, setActiveDragId] = useState(null);

  // Get unique hotel names for this guide's pilgrims
  const myHotelNames = [...new Set(myPilgrims.map((p) => p.hotel))];

  // Get check-in dates for selected hotel
  let availableDates = [];
  if (selectedHotel) {
    availableDates = [...new Set(myPilgrims.filter(p => p.hotel === selectedHotel).map(p => p.checkin))];
  }

  // Get pilgrims for selected hotel and date
  let pilgrimsForHotelDate = [];
  if (selectedHotel && selectedDate) {
    pilgrimsForHotelDate = myPilgrims.filter(p => p.hotel === selectedHotel && p.checkin === selectedDate);
  }

  // Find hotel object for selectedHotel
  const hotelObj = localHotels.find(h => h.name === selectedHotel);

  // Find rooms for this guide, hotel, and date
  let myRooms = [];
  if (hotelObj && selectedDate) {
    myRooms = hotelObj.rooms.filter(
      room =>
        room.guideId === guideId &&
        room.checkin === selectedDate
    );
  }

  // Drag and drop handlers
  function handleDragStart(event) {
    setActiveDragId(event.active.id);
  }
  function handleDragEnd(event) {
    setActiveDragId(null);
    const {active, over} = event;
    if (!over) return;
    const pilgrimId = parseInt(active.id.replace('pilgrim-', ''));
    const roomId = parseInt(over.id.replace('room-', ''));
    // Find the hotel and room
    setLocalHotels(prevHotels => prevHotels.map(hotel => {
      if (hotel.name !== selectedHotel) return hotel;
      return {
        ...hotel,
        rooms: hotel.rooms.map(room => {
          if (
            room.roomId === roomId &&
            room.guideId === guideId &&
            room.checkin === selectedDate &&
            !room.assignedPilgrims.includes(pilgrimId) &&
            room.assignedPilgrims.length < room.capacity
          ) {
            return {
              ...room,
              assignedPilgrims: [...room.assignedPilgrims, pilgrimId]
            };
          }
          // Remove from other rooms for this guide/date
          if (room.assignedPilgrims.includes(pilgrimId) && room.guideId === guideId && room.checkin === selectedDate) {
            return {
              ...room,
              assignedPilgrims: room.assignedPilgrims.filter(pid => pid !== pilgrimId)
            };
          }
          return room;
        })
      };
    }));
  }

  // Pilgrims not assigned to any room for this hotel/date
  let assignedIds = [];
  if (myRooms.length > 0) {
    assignedIds = myRooms.flatMap(room => room.assignedPilgrims);
  }
  const unassignedPilgrims = pilgrimsForHotelDate.filter(p => !assignedIds.includes(p.pilgrimId));

  return (
    <DndContext onDragEnd={handleDragEnd} onDragStart={handleDragStart}>
  <div className='flex flex-col items-start justify-center p-10 gap-4'>
        <h1 className='text-2xl font-bold mb-4'>Guide:<br/> {guideName}</h1>
        <h2 className='text-xl font-semibold mb-2'>Hotels:</h2>
        <div className='flex gap-4 mb-6'>
          {myHotelNames.length === 0 && <p>No hotels assigned to your pilgrims.</p>}
          {myHotelNames.map(hotel => (
            <button
              key={hotel}
              className={`border rounded p-4 bg-white shadow hover:bg-blue-100 transition ${selectedHotel === hotel ? 'ring-2 ring-blue-500' : ''}`}
              onClick={() => { setSelectedHotel(hotel); setSelectedDate(null); }}
            >
              {hotel}
            </button>
          ))}
        </div>
        {selectedHotel && (
          <div className='mb-6'>
            <h2 className='text-lg font-semibold mb-2'>Check-in Dates for {selectedHotel}:</h2>
            <div className='flex gap-4'>
              {availableDates.map(date => (
                <button
                  key={date}
                  className={`border rounded p-2 bg-white hover:bg-green-100 transition ${selectedDate === date ? 'ring-2 ring-green-500' : ''}`}
                  onClick={() => setSelectedDate(date)}
                >
                  {date}
                </button>
              ))}
            </div>
          </div>
        )}
        {selectedHotel && selectedDate && (
          <div className='w-full'>
            <h2 className='text-lg font-semibold mb-2'>Your Room(s) for {selectedHotel} on {selectedDate} :</h2>
            <div className='flex gap-4 flex-wrap'>
              {myRooms.length === 0 ? (
                <p>No rooms assigned to your pilgrims for this date.</p>
              ) : (
                myRooms.map(room => (
                  <DroppableRoom key={room.roomId} room={room} pilgrims={pilgrims} />
                ))
              )}
            </div>
            <div className='mt-4'>
              <h3 className='font-semibold mb-1'>Unassigned pilgrims for this date:</h3>
              <div className='flex gap-2 flex-wrap'>
                {unassignedPilgrims.length === 0 ? (
                  <p>All pilgrims are assigned to rooms.</p>
                ) : (
                  unassignedPilgrims.map(p => (
                    <DraggablePilgrim key={p.pilgrimId} pilgrim={p} />
                  ))
                )}
              </div>
            </div>
          </div>
        )}
      </div>
      <DragOverlay>
        {activeDragId ? (
          (() => {
            const pid = parseInt(activeDragId.replace('pilgrim-', ''));
            const pilgrim = pilgrims.find(p => p.pilgrimId === pid);
            return pilgrim ? (
              <div className="border rounded p-2 bg-white shadow-2xl min-w-[100px] text-center scale-110 z-50 transition-all duration-200">
                {pilgrim.name}
              </div>
            ) : null;
          })()
        ) : null}
      </DragOverlay>
    </DndContext>
  );
}

// Draggable pilgrim card
function DraggablePilgrim({ pilgrim }) {
  const { attributes, listeners, setNodeRef, isDragging } = useDraggable({
    id: `pilgrim-${pilgrim.pilgrimId}`,
  });
  return (
    <div
      ref={setNodeRef}
      {...attributes}
      {...listeners}
      className={`border rounded p-2 bg-white shadow cursor-move min-w-[100px] text-center transition-all duration-200 ${isDragging ? 'scale-110 z-20 shadow-2xl opacity-80' : ''}`}
      style={{ marginBottom: 8 }}
    >
      {pilgrim.name}
    </div>
  );
}

// Droppable room card
function DroppableRoom({ room, pilgrims }) {
  const { setNodeRef, isOver } = useDroppable({
    id: `room-${room.roomId}`,
  });
  const isFull = room.assignedPilgrims.length >= room.capacity;
  return (
    <div
      ref={setNodeRef}
      className={`border p-4 rounded mb-4 bg-gray-50 min-w-[200px] ${isOver ? 'ring-2 ring-green-500' : ''} ${isFull ? 'opacity-60' : ''}`}
    >
      <div className='font-medium mb-1'>Room {room.roomId}</div>
      <div>Capacity: {room.capacity}</div>
      <div>Assigned: {room.assignedPilgrims.length} {isFull && <span className='text-red-500'>(Full)</span>}</div>
      <div className='mt-1'>
        <span className='font-semibold'>People in this room:</span>
        <ul className='list-disc ml-5'>
          {room.assignedPilgrims.map(pid => {
            const pilgrim = pilgrims.find(p => p.pilgrimId === pid);
            return <li key={pid}>{pilgrim ? pilgrim.name : `Pilgrim #${pid}`}</li>;
          })}
        </ul>
      </div>
    </div>
  );
}

export default GuidesPage